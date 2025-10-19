import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import {ACCESS_TOKEN, REFRESH_TOKEN} from "../constants";
import "../styles/Form.css";
import LoadingIndicator from "../pages/LoadingIndicator";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault(); // prevent page reload
        
        // send a request to the backend, either to login or register
        try {
            const res = await api.post(route, { username, password });
            if (method === "login") {
                // store the tokens in local storage
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/"); // redirect to home page
            } else {
                // after registering, go to login page
                navigate("/login"); // redirect to login page
            }
        } catch (error) {
            console.error("Error during form submission:", error);
            alert("An error occurred. Please try again.");
        } finally {
            setLoading(false);
        }   
    }

    return <form onSubmit={handleSubmit} className="form-container">
            <h1>{name} Form</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
                required
            />
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
            />
            {loading && <LoadingIndicator />}
            <button className="form-button" type="submit">
                {name}
            </button>
        </form>
}

export default Form;