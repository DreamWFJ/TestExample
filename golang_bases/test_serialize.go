package main

import (
	"encoding/gob"
	"encoding/xml"
	"fmt"
	"os"
)

type StudentB struct {
	Name string
	Age int
}

func test_serialize_1()  {
	//序列号和反序列化
	s := &StudentB{"张三", 19}
	f, err := os.Create("2.txt")
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	defer f.Close()
	encode := gob.NewEncoder(f)
	encode.Encode(s)
	f.Seek(0, os.SEEK_SET)
	decoder := gob.NewDecoder(f)
	var s1 StudentB
	decoder.Decode(&s1)
	fmt.Println(s1)
}

func test_serialize_2()  {
	//将xml序列化的数据存入文件
	f, err := os.Create("data.dat")
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	defer f.Close()
	s := &StudentB{"张三", 19}
	encoder := xml.NewEncoder(f)
	encoder.Encode(s)
	f.Seek(0, os.SEEK_SET)
	decoder := xml.NewDecoder(f)
	var s1 StudentB
	decoder.Decode(&s1)
	fmt.Println(s1)
}


func test_serialize_3()  {
	//直接XML序列化后输出
	s := &StudentB{"张三", 19}
	result, err := xml.Marshal(s)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	fmt.Println(string(result))
}

func test_serialize_4()  {
	//将xml文件反序化
	str := `<?xml version="1.0" encoding="utf-8"?><StudentB><Name>张三</Name><Age>19</Age></StudentB>`
	var s StudentB
	xml.Unmarshal([]byte(str), &s)
	fmt.Println(s)
}

type StudentC struct {
	XMLName xml.Name `xml:"student"`
	Name string `xml:"name,attr"`
	Age int `xml:"age,attr"`
	Phone []string `xml:"phones>phone"`
}

type ABC string

func test_serialize_5()  {
	str := `<?xml version="1.0" encoding="utf-8"?>
	<student name="张三" age="19">
	<phones>
		<phone>18612082212</phone>
		<phone>13641361488</phone>
	</phones>
	</student>`
	var s StudentC
	xml.Unmarshal([]byte(str), &s)
	fmt.Println(s)
}
func main()  {
	//test_serialize_1()
	//test_serialize_2()
	//test_serialize_3()
	//test_serialize_4()
	test_serialize_5()
}