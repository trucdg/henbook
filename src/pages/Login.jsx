
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";
import Form from "../components/Form";

function Login() {
  const navigate = useNavigate();
  useEffect(() => {
    // If access token exists, redirect to home
    if (localStorage.getItem(ACCESS_TOKEN)) {
      navigate("/");
    }
  }, [navigate]);
  return (
    <Form route="/api/token/" method="login" />
  );
}

export default Login;