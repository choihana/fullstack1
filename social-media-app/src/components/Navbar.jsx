import React from "react"
import { Container, Nav, NavDropdown, Navbar, Image } from "react-bootstrap"
import { useUserActions } from "../hooks/user.action"
import { randomAvatar } from "../utils";

function Navigationbar() {
    const userActions = useUserActions();
    const handleLogout = () => {
    userActions.logout()
    }
	
        return (
		    <Navbar bg="primary" variant="dark">
			    <Container>
				    <Navbar.Brand className="fw-bold" href="#home">
					    Postagram
				    </Navbar.Brand>
				    <Navbar.Collapse className="justify-content-end">
					    <Nav>
						    <NavDropdown
							title={<Image src={randomAvatar()} roundedCircle width={36} height={36} />}>
                            <NavDropdown.Item href="#">Profile
                            </NavDropdown.Item>
                            <NavDropdown.Item onClick={handleLogout}>
                            Logout</NavDropdown.Item>
                            </NavDropdown>
					    </Nav>
				        </Navbar.Collapse>
			    </Container>
		    </Navbar>
	    )
}

export default Navigationbar