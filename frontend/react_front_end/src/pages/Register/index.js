import { Button, Card, Col, Form, Input, Row } from "antd";
import { useNavigate } from "react-router-dom";
import { register } from "../../Services/userService";
// import { checkExists, register } from "../../Services/userService";
// import { generateToken } from "../../helpers/generateToken";

function Register() {
    const navigate = useNavigate();

    const rules = [
        {
            required: true, 
            message: 'Bắt buộc!'
        }
    ];

    const onFinish = async (e) => {
        // const checkExistsEmail = await checkExists("email", e.email);
        // if (checkExistsEmail.length > 0) {
        //     alert("Email đã tồn tại");
        // } else {

        const options = {
            username: e.username,
            email: e.email,
            password: e.password
            // token: generateToken()
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