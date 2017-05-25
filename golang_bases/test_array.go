package main
import "fmt"
import "reflect"

func main(){
	p := [...]int{2,3,4,5,6,7}
	s1 := p[1:3]
	fmt.Println(s1)
	fmt.Println(reflect.TypeOf(p))
	fmt.Println(reflect.TypeOf(s1))
	for _, v := range p {
		fmt.Println(v)
	}
}
