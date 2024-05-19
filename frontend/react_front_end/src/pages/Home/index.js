import { Button, Col, Flex, Row, Select, message } from "antd";
import { SwapOutlined, SoundOutlined, CopyOutlined, StarFilled } from "@ant-design/icons";
import { useEffect, useState } from "react";
import "../../language";
import { language } from "../../language";
import TextArea from "antd/es/input/TextArea";
import { getCookie} from "../../helpers/cookie";
import { translateTextServer,  saveRecord } from "../../Services/userService";


function Home() {
    const token = getCookie("token");

    const [messageApi, contextHolder] = message.useMessage();

    const [FromLang, setFromLang] = useState({ value: 'en-GB', label: language['en-GB'] });
    const [ToLang, setToLang] = useState({ value: 'vi-VN', label: language['vi-VN'] });

    const [inputText, setInputText] = useState('');
    const [translatedText, setTranslatedText] = useState('');

    const languageOptions = Object.keys(language).map((key) => ({
        label: language[key],
        value: key,
    }));

    const translateText = async (text) => {
        let mapping = {
            'English': 'en-GB',
            'Vietnamese': 'vi-VN'
        }
        const options = {
            from_language: mapping[FromLang.label],
            to_language: mapping[ToLang.label],
            from_content: text,
            engine: 'auto'
        }
        const response = await translateTextServer(options);
        if (response.ok) {
            const data = await response.json();
            setTranslatedText(data.to_content);
        } else {
            try {
                setTranslatedText(response.text());
            }
            catch {
                setTranslatedText('Exception');
            }
        }

    };

    const SwapLang = () => {
        let temp = FromLang;
        setFromLang(ToLang);
        setToLang(temp);

        let tempText = inputText;
        setInputText(translatedText);
        setTranslatedText(tempText);
    }

    const handleChangeFromLang = (label, value) => {
        setFromLang({ value: label, label: value });
    }

    const handleChangeToLang = (value, option) => {
        setToLang({ value: option, label: option });
    }

    const SpeakInputText = () => {
        const synth = window.speechSynthesis;
        const utterThis = new SpeechSynthesisUtterance(inputText);
        utterThis.lang = FromLang.label;
        synth.speak(utterThis);
    }

    const SpeakTranslatedText = () => {
        const synth = window.speechSynthesis;
        const utterThis = new SpeechSynthesisUtterance(translatedText);
        utterThis.lang = ToLang.label;
        synth.speak(utterThis);
    }

    const Copy = () => {
        navigator.clipboard.writeText(translatedText);
    }

    const Save = async () => {
        const options = {
            to_content: translatedText,
            engine_used: "google",
            from_language: FromLang.value,
            to_language: ToLang.value,
            from_content: inputText,
        }

        const save = await saveRecord(options);
        console.log(save);
        if (save) {
            messageApi.open({
                type: 'success',
                content: "Lưu thành công, vào mục 'bản dịch đã lưu' để xem chi tiết"
            });
        } else {
            messageApi.open({
                type: 'error',
                content: "Lưu thất bại"
            });
        }
    }

    useEffect(() => {
        if (inputText) {
            translateText(inputText);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [inputText, translatedText, ToLang.label]);

    return (
        <>
            {contextHolder}
            <Flex justify="center">
                <Select
                    onChange={handleChangeFromLang}
                    options={languageOptions}
                    value={FromLang.label}
                    defaultValue={language['en-GB']}
                    className="select__lang"
                />
                <div className="swap select__lang"><SwapOutlined onClick={SwapLang} /></div>
                <Select
                    onChange={handleChangeToLang}
                    options={languageOptions}
                    value={ToLang.label}
                    defaultValue={language['vi-VN']}
                    className="select__lang"
                />
            </Flex>

            <Flex justify="space-around">
                <Row gutter={[12, 12]}>
                    <Col xl={12}>
                        <TextArea
                            value={inputText}
                            allowClear
                            rows={8}
                            cols={70}
                            className="margin-right"
                            onChange={(e) => setInputText(e.target.value)}
                        />
                        <div className="btn fromlang">
                            <Button shape="circle" onClick={SpeakInputText}>
                                <SoundOutlined />
                            </Button>
                            {token && translatedText !== "" ? (
                                <>
                                    <Button shape="circle" onClick={Save}>
                                        <StarFilled />
                                    </Button>
                                </>
                            ) : (<></>)}
                        </div>
                    </Col>
                    <Col xl={12}>
                        <TextArea
                            value={translatedText}
                            rows={8}
                            cols={70}
                            readOnly
                            className="text"
                        />
                        <div className="btn tolang">
                            <Button shape="circle" onClick={SpeakTranslatedText}>
                                <SoundOutlined />
                            </Button>
                            <Button shape="circle" onClick={Copy}>
                                <CopyOutlined />
                            </Button>
                        </div>
                    </Col>
                </Row>
            </Flex>
        </>
    )
}

export default Home;