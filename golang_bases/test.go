package main
import "fmt"

func main(){
	var arr_1 [2]int
	arr_2 := [2]int{}
	arr_3 := [2]int{1, 2}
	arr_3_1 := [2]int{0:1, 1:2}
	arr_4 := [...]int{1,2}
	arr_5 := [...]int{3:9}
	fmt.Println(arr_1)
	fmt.Println(arr_2)
	fmt.Println(arr_3)
	fmt.Println(arr_3_1)
	fmt.Println(arr_4)
	fmt.Println(arr_5)
	const PI = 3.1415926
	const y = "Hello"
	fmt.Println(PI, y)
	const (
			Sunday = iota
			Monday
			Tuesday
			A2 = "gg"
			Thirsday = iota
			Friday
			)
	fmt.Println("Sunday=", Sunday, "Monday=",Monday, "Tuesday=",Tuesday, "A2=",A2, "Thirsday=",Thirsday)
	if a:=2; a < 2 {
		fmt.Println("a<2")
	}else{
		fmt.Println("a=",a)
	}
	i := 5
	switch i {
		case 1:
			fmt.Println("i is equal to 1")
		case 2:
			fmt.Println("i is equal to 2")
		case 3,4,5,6:
			fmt.Println("i is equal to 3,4,5 or 6")
			fallthrough
		default:
			fmt.Println("others")


	}
	
	str := "Hello World!"
	for i,j := 0, len(str); i<j; i++ {
		fmt.Println(string(str[i]))
	}
}
