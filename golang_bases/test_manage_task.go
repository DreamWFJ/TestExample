package main

import (
	"fmt"
	"runtime"
	"time"
)

func SayHello()  {
	for i := 0; i < 10; i++ {
		fmt.Print("Hello")
		runtime.Gosched()
	}
}

func SayWorld()  {
	for i := 0; i < 10; i++ {
		fmt.Println("World!")
		runtime.Gosched()
	}
}

func test()  {
	defer func() {
		fmt.Println("in defer!")
	}()
	for i := 0; i < 10; i++ {
		fmt.Println(i)
		if i < 5 {
			runtime.Goexit()
		}
	}
}

func producer(c chan <- int)  {
	defer close(c)
	for i := 0; i < 10; i++ {
		c <- i
	}
}

func consumer(c <- chan int, f chan <- int)  {
	for {
		if v, ok := <- c; ok {
			fmt.Println(v)
		} else {
			break
		}
	}
	//for v := range c {
	//	fmt.Println(v)
	//}
	f <- 1
}

func test_2e()  {
	n := runtime.GOMAXPROCS(runtime.NumCPU())
	fmt.Println(n)
	go test()
	//var str string
	//fmt.Scan(&str)
	//time.Sleep(1 * time.Second)
}

func test_3e()  {
	go SayHello()
	go SayWorld()
	time.Sleep(5 * time.Second)
	fmt.Println(runtime.NumCPU())
	fmt.Println(runtime.NumGoroutine())
}

func test_4e()  {
	buf := make(chan int)
	flg := make(chan int)
	go producer(buf)
	go consumer(buf, flg)
	<- flg
	fmt.Println("Test channel")
}

func test_5e()  {
	c := make(chan int, 2)
	c <- 1
	c <- 2
	fmt.Println(<-c)
	fmt.Println(<-c)
}

func fibonacci(c, quit chan int)  {
	x, y := 0, 1
	for {
		select {
		case c <- x:
			x, y = y, x+y
			fmt.Println("received data: x=", x, " y=",y)
		case <-quit:
			fmt.Println("quit")
			return
		}
	}
}

func test_6e()  {
	c := make(chan int)
	quit := make(chan int)
	go func() {
		for i := 0; i < 10; i++ {
			fmt.Println(<- c)
		}
		quit <- 0
	}()
	fibonacci(c, quit)
}

func test_7e()  {
	c := make(chan int)
	select {
	case <- c:
		fmt.Println("received data")
	case <- time.After(5 * time.Second):
		fmt.Println("time out")

	}
}
func main()  {
	//test_2e()
	//test_3e()
	//test_4e()
	//test_5e()
	test_6e()
	//test_7e()
}