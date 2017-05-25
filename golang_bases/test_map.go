package main
import "fmt"

func main(){
	mp := make(map[string]string)
	mp["a"] = "1"
	mp["b"] = "123445"
	mp["sh"] = "ShangHai"
	v, ok := mp["sh"]
	if ok {
		fmt.Println(v)
	} else {
		fmt.Println("key'sh don't exist!")
	}
	fmt.Println(mp)
}
