package main

import "fmt"

type MyFuncType func(int)bool

func isBigThan5(n int)bool {
	return n > 5
}

func Display(arr []int, f MyFuncType){
	for _, v := range arr {
		if f(v) {
			fmt.Println(v)
		}
	}
}

func Test()  {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println(err)
		}
	}()
	divide1(5, 0)
	fmt.Println("end of test")
}

func divide1(a, b int) int {
	return a/b
}
func main()  {
	arr := []int{1,2,3,4,5,6,7,8}
	Display(arr, isBigThan5)
	Test()
}