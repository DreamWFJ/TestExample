package main
import (
	"fmt"
	"time"
)

func test_date_1()  {
	fmt.Println(time.Now().Format("2006-01-02 15:04:05"))
}

func test_date_2()  {
	d, err := time.Parse("01-02-2006", "08-17-2013")
	if err != nil {
		fmt.Println(err.Error())
	}
	fmt.Println(d)
}

func test_date_3()  {
	t := time.Now()
	t2 := t.Add(24 * time.Hour)
	d := t2.Sub(t)
	fmt.Println(t)
	fmt.Println(t2)
	fmt.Println(d)
	if t.Before(t2){
		fmt.Println("t < t2")
	}
	if t2.After(t) {
		fmt.Println("t2 < t")
	}
	if t.Equal(t){
		fmt.Println("t = t")
	}
}

func test_timer_1()  {
	fmt.Println(time.Now())
	c := time.After(10 * time.Second)
	t := <- c
	fmt.Println(t)
	tm := time.NewTimer(10 * time.Second)
	t = <- tm.C
	fmt.Println(t)
}
func show_time_now()  {
	fmt.Println("Hello world!", time.Now())
}
func test_timer_2()  {
	fmt.Println(time.Now())
	time.AfterFunc(10 * time.Second, show_time_now)
	var str string
	fmt.Scan(&str)
}

func test_timer_3()  {
	c := time.Tick(10 * time.Second)
	for t := range c {
		fmt.Println(t)
	}
}

func main()  {
	//test_date_1()
	//test_date_2()
	//test_date_3()
	//test_timer_1()
	//test_timer_2()
	test_timer_3()
}
