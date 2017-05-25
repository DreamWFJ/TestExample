package main

import (
	"net"
	"fmt"
)

func test_udp_server()  {
	addr, err := net.ResolveUDPAddr("udp", ":7070")
	if err != nil {
		fmt.Println(err)
		return
	}
	conn, err1 := net.ListenUDP("udp", addr)
	if err1 != nil {
		fmt.Println(err1)
		return
	}
	for {
		var buf[1024]byte
		n, addr, err := conn.ReadFromUDP(buf[0:])
		if err != nil {
			fmt.Println(err)
			return
		}
		go HandleClient(conn, buf[0:n], addr)
	}
}

func HandleClient(conn *net.UDPConn, data []byte, addr *net.UDPAddr)  {
	fmt.Println("receive: " + string(data))
	conn.WriteToUDP([]byte("ok, data has been received"), addr)
}

func test_udp_client()  {
	addr, err := net.ResolveUDPAddr("udp", "127.0.0.1:7070")
	if err != nil {
		fmt.Println(err)
		return
	}

	conn, err1 := net.DialUDP("udp", nil, addr)
	if err1 != nil {
		fmt.Println(err1)
		return
	}
	defer conn.Close()
	conn.Write([]byte("Hello Server"))
	var buf [1024]byte
	n, _, err2 := conn.ReadFromUDP(buf[0:])
	if err2 != nil {
		fmt.Println(err1)
		return
	}
	fmt.Println(string(buf[0:n]))
}

func main()  {
	test_udp_client()
	//test_udp_server()
}