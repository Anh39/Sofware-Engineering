import { Button, Card, Col, Flex, Form, Input, Row, message } from "antd";

function ResetPassword() {
    const rules = [
        {
            required: true,
            message: 'Bắt buộc!'
        }
    ];

    const onFinish = async (e) => {
        console.log(e);
        const { username, oldPassword, newPassword, repeateNewPassword } = e;

        if (newPassword !== repeateNewPassword) {
            message.error("Mật khẩu mới và viết lại mật khẩu mới không khớp");
            return;
        }

        const response = await fetch("http://localhost:8080/api/user/reset-password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                oldPassword,
                newPassword
            })
        });

        // nên viết lại cái response

        if (response.ok) {
            message.success("Đặt lại mật khẩu thành công");
        } else {
            message.error("Đặt lại mật khẩu thất bại");
        }
    }
    return (
        <>
            <Flex justify="center">
                <Row gutter={[20, 20]}>
                    <Col span={12}>
                        <Card title="Đặt lại mật khẩu">
                            <Form onFinish={onFinish}>
                                <Form.Item label="username" name="username" rules={rules} >
                                    <Input />
                                </Form.Item>
                                <Form.Item label="Mật khẩu cũ" name="oldPassword" rules={rules} >
                                    <Input.Password />
                                </Form.Item>
                                <Form.Item label="Mật khẩu mới" name="newPassword" rules={rules} >
                                    <Input.Password />
                                </Form.Item>
                                <Form.Item label="Viết lại mật khẩu mới" name="repeateNewPassword" rules={rules} >
                                    <Input.Password />
                                </Form.Item>
                                <Form.Item>
                                    <Button type="primary" htmlType="submit">
                                        Đặt lại mật khẩu
                                    </Button>
                                </Form.Item>
                            </Form>
                        </Card>
                    </Col>
                </Row>
            </Flex>
        </>
    )
}

export default ResetPassword;