package main

import (
	"net"
	"fmt"
	"os"
	"io/ioutil"
	"bytes"
	"bufio"
	"strings"
)

func test_tcp_1()  {
	//获取接口地址
	addr, err := net.InterfaceAddrs()
	if err != nil {
		fmt.Println(err)
	};
	fmt.Println(addr)

	//获取主机对应IP地址
	ips, err := net.LookupIP("www.baidu.com")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(ips)
}

func test_tcp_2()  {
	//创建TCPAddr
	ip, err := net.ResolveTCPAddr("tcp", "www.baidu.com:80")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(ip)
}

const (
	LS = "LS"
	CD = "CD"
	PWD = "PWD"
	QUIT = "QUIT"
)

func test_tcp_server()  {
	tcpAddr, err := net.ResolveTCPAddr("tcp", ":7076")
	checkError(err)
	listener, err1 := net.ListenTCP("tcp", tcpAddr)
	checkError(err1)
	for {
		conn, err2 := listener.Accept()
		if err2 != nil {
			fmt.Println(err2)
			continue
		}
		fmt.Println("receive client request")
		go ServeClient(conn)
	}
}

func test_tcp_client()  {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Println("please input cmd:")
		line, err := reader.ReadString('\n')
		checkError(err)
		line = strings.TrimSpace(line)
		line = strings.ToUpper(line)
		arr := strings.SplitN(line, " ", 2)
		fmt.Println(arr)
		switch arr[0] {
		case LS:
			SendRequest(LS)
		case CD:
			SendRequest(CD + " " + strings.TrimSpace(arr[1]))
		case PWD:
			SendRequest(PWD)
		case QUIT:
			fmt.Println("program exit")
			return
		default:
			fmt.Println("cmd error")
		}
	}
}

func SendRequest(cmd string)  {
	tcpAddr, err := net.ResolveTCPAddr("tcp", "127.0.0.1:7076")
	checkError(err)
	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	checkError(err)
	SendData(conn, cmd)
	fmt.Println(ReadData(conn))
	conn.Close()
}


func ServeClient(conn net.Conn)  {
	defer conn.Close()
	str := ReadData(conn)
	if str == "" {
		SendData(conn, "receive data error")
		return
	}
	fmt.Println("receive cmd: ", str)
	switch str {
	case LS:
		ListDir(conn)
	case PWD:
		Pwd(conn)
	default:
		if str[0:2] == CD {
			Chdir(conn, str[3:])
		} else {
			SendData(conn, "cmd error")
		}
	}
}

func Chdir(conn net.Conn, s string)  {
	err := os.Chdir(s)
	if err != nil {
		SendData(conn, err.Error())
	} else {
		SendData(conn, "ok")
	}
}

func ListDir(conn net.Conn)  {
	files, err := ioutil.ReadDir(".")
	if err != nil {
		SendData(conn, err.Error())
		return
	}
	var str string
	for i, j := 0, len(files); i < j; i++ {
		f := files[i]
		str += f.Name() + "\t"
		if f.IsDir() {
			str += "dir\r\n"
		} else {
			str += "file\r\n"
		}
	}
	SendData(conn, str)
}

func ReadData(conn net.Conn) string {
	var data bytes.Buffer
	var buf [512]byte
	for {
		n, err := conn.Read(buf[0:])
		if err != nil {
			fmt.Println(err)
			return ""
		}
		//以0作为结束标志
		if buf[n-1] == 0 {
			data.Write(buf[0 : n-1])
			break
		} else {
			data.Write(buf[0:n])
		}
	}
	return string(data.Bytes())
}

func SendData(conn net.Conn, data string)  {
	buf := []byte(data)
	buf = append(buf, 0)
	_, err := conn.Write(buf)
	if err != nil {
		fmt.Println(err)
	}
}

func Pwd(conn net.Conn)  {
	s, err := os.Getwd()
	if err != nil {
		SendData(conn, err.Error())
	} else {
		SendData(conn, s)
	}
}

func checkError(err error)  {
	if err != nil {
		fmt.Println(err)
		os.Exit(0)
	}
}
func main()  {
	//test_tcp_1()
	//test_tcp_2()
	//分别启动服务端和客户端，可以通信
	//test_tcp_server()
	test_tcp_client()
}