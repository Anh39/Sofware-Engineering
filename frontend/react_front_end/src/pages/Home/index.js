import { Button, Col, Flex, Row, Select } from "antd";
import { ZhihuOutlined, PaperClipOutlined, SwapOutlined, SoundOutlined } from "@ant-design/icons";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../../language";
import { language } from "../../language";
import TextArea from "antd/es/input/TextArea";

function Home() {
    const [FromLang, setFromLang] = useState({ value: 'en-GB', label: language['en-GB'] });
    const [ToLang, setToLang] = useState({ value: 'vi-VN', label: language['vi-VN'] });

    const [inputText, setInputText] = useState('');
    const [translatedText, setTranslatedText] = useState('');

    const languageOptions = Object.keys(language).map((key) => ({
        label: language[key],
        value: key,
    }));

    const [selectedButton, setSelectedButton] = useState("");

    const handleClick = (buttonType) => {
        setSelectedButton(buttonType);
    }

    const translateText = async (text) => {
        const apiUrl = `https://api.mymemory.translated.net/get?q=${text}&langpair=${FromLang.label}|${ToLang.label}`;
        const response = await fetch(apiUrl);
        const data = await response.json();
        if (data.responseData) {
            setTranslatedText(data.responseData.translatedText);
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
        console.log(label, value);
        setFromLang({ value: label, label: value });
    }

    const handleChangeToLang = (value, option) => {
        console.log(value, option);
        setToLang({ value: option, label: option });
    }

    useEffect(() => {
        if (inputText) {
            translateText(inputText);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [inputText, translatedText]);

    return (
        <>
            <Flex className="trans__type" gap="large">
                <Button className={`trans__type--button ${selectedButton === "text" ? "selected" : ""}`} onClick={() => handleClick("text")} >
                    <Link to="/"><ZhihuOutlined /> Dịch văn bản</Link>
                </Button>
                <Button className={`trans__type--button ${selectedButton === "document" ? "selected" : ""}`} onClick={() => handleClick("document")} >
                    <Link to="/docs"><PaperClipOutlined /> Dịch tài liệu</Link>
                </Button>
            </Flex>

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
                        <SoundOutlined />
                    </Col>
                    <Col xl={12}>
                        <TextArea
                            value={translatedText}
                            rows={8}
                            cols={70}
                            readOnly
                            className="text"
                        />
                    </Col>
                </Row>
            </Flex>
        </>
    )
}

export default Home;