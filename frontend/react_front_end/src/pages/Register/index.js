import { Button, Card, Col, Form, Input, Row } from "antd";
import { useNavigate } from "react-router-dom";
import { checkExists, register } from "../../Services/userService";
import { generateToken } from "../../helpers/generateToken";

function Register() {
    const navigate = useNavigate();

    const rules = [
        {
            required: true, 
            message: 'Bắt buộc!'
        }
    ];

    const onFinish = async (e) => {
        const checkExistsEmail = await checkExists("email", e.email);
        if (checkExistsEmail.length > 0) {
            alert("Email đã tồn tại");
        } else {
            const options = {
                username: e.username,
                email: e.email,
                password: e.password,
                token: generateToken()
            };
            const response = await register(options);
            console.log(response);
            if (response) {
                navigate("/login");
            } else {
                alert("Sai tài khoản hoặc mật khẩu");
            }
        }
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
                            <Form.Item label="Số điện thoại" name="phone" rules={rules}>
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