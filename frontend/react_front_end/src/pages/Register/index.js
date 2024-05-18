import { Button, Card, Col, Form, Input, Row } from "antd";
import { useNavigate } from "react-router-dom";
import { register } from "../../Services/userService";

function Register() {
    const navigate = useNavigate();

    const rules = [
        {
            required: true, 
            message: 'Bắt buộc!'
        }
    ];

    const onFinish = async (e) => {
        const options = {
            username: e.username,
            email: e.email,
            password: e.password
        };
        console.log(e.username);
        const response = await register(options);
        console.log(console);
        if (response.ok) {
            const data = await response.json();
            if (data.success === true) {
                navigate("/login");
                return
            }
        }
        alert("Tài khoản hoặc email đã tồn tại");

        // }
    }

    return (
        <>
            <Row justify="center">
                <Col span={12}>
                    <Card title="Đăng kí tài khoản">
                        <Form onFinish={onFinish} layout="vertical">
                            <Form.Item label="Email" name="email" rules={rules}>
                                <Input />
                            </Form.Item>
                            <Form.Item label="Username" name="username" rules={rules}>
                                <Input />
                            </Form.Item>
                            <Form.Item label="Password" name="password" rules={rules}>
                                <Input.Password />
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit">
                                    Đăng kí
                                </Button>
                            </Form.Item>
                        </Form>
                    </Card>
                </Col>
            </Row>
        </>
    )
}

export default Register;