import Form from "../components/Form";

function Register() {
  return (
    // ensure trailing slash to avoid Django redirect that can convert POST -> GET
    <Form route="/api/user/register/" method="register" />
  );
}

export default Register;