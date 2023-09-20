import axios from "axios"
import createAuthRefreshInterceptor from "axios-auth-refresh";
import { getAccessToken, getRefreshToken, getUser } from "../hooks/user.action"

const axiosService = axios.create({
    baseURL: "http://localhost:8000/api",
    headers:{
        "Content-Type": "application/json",
    },
});

axiosService.interceptors.request.use(async(config) =>{
    // 로컬 스토리지에서 액세스 토큰을 가져와 요청의 헤더에 추가

    // const {access} = JSON.parse(localStorage.getItem("auth"));
    // config.headers.Authorization = `Bearer ${access}`;
    config.headers.Authorization = `Bearer ${getAccessToken()}`
    return config;
});

axiosService.interceptors.response.use(
    (res) =>Promise.resolve(res),
    (err) =>Promise.reject(err)
)

const refreshAuthLogic = async (failedRequest) => {
	const { refresh } = JSON.parse(localStorage.getItem("auth"))
	return axios
        .post("/auth/refresh/", {
            refresh: getRefreshToken(),},
            {baseURL:"http://localhost:8000/api",}
            
            )
		// .post("/refresh/token/", null, {
		// 	baseURL: "http://localhost:8000",
		// 	headers: {
		// 		Authorization: `Bearer ${refresh}`,
		// 	},
		// })
		.then((resp) => {
			const { access } = resp.data
			failedRequest.response.config.headers["Authorization"] =
				"Bearer " + access
			localStorage.setItem(
				"auth",
				JSON.stringify({
					access,
					refresh: getRefreshToken(), 
                    user:getUser()
				})
			)
		})
		.catch(() => {
			localStorage.removeItem("auth")
		})
}

//토큰이 만료되었을때 자동으로 갱신하여 사용자가 로그인된 상태를 유지할 수 있도록 해줌 
createAuthRefreshInterceptor(axiosService, refreshAuthLogic)

//주어진 url에 get요청을 보내고 응답 데이터를 반환
export function fetcher(url) {
	return axiosService.get(url).then((res) => res.data)
}

export default axiosService