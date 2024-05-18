import { Button, Card, Col, Form, Input, Row } from "antd";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { setCookie } from "../../helpers/cookie";
import { checkLogin } from "../../actions/login";
import { login } from "../../Services/userService";


function Login() {
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const rules = [
        {
            required: true,
            message: 'Bắt buộc!'
        }
    ];

    const onFinish = async (e) => {
        const options = {
            username: e.username,
            password: e.password
        }
        const response = await login(options);
        if (response.ok) {
            const data = await response.json();
            if (data.success === true) {
                // setCookie("id", data.id, 1);
                // setCookie("username", data.username, 1);
                // setCookie("email", data.email, 1);
                setCookie("token", data.token, 1);
                //document.cookie = `token=${data.token};path=/;`

                dispatch(checkLogin(true));
                navigate("/");
                return
            }
        }
        alert("Login failed");

    }
    return (
        <>
            <Row justify="center">
                <Col span={12}>
                    <Card title="Đăng nhập">
                        <Form onFinish={onFinish} layout="vertical">
                            <Form.Item label="Username" name="username" rules={rules}>
                                <Input />
                            </Form.Item>

                            <Form.Item label="Password" name="password" rules={rules}>
                                <Input.Password />
                            </Form.Item>

                            <Form.Item>
                                <Button type="primary" htmlType="submit">
                                    Đăng nhập
                                </Button>
                            </Form.Item>
                        </Form>
                    </Card>
                </Col>
            </Row>
        </>
    )
}

export default Login;