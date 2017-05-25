package main
import "fmt"
import "os"

func divide(a, b int)(int, int){
	quotient := a/b
	remainder := a%b
	return quotient, remainder
}

func sum(aregs ...int)int{
	s := 0
	for _, number := range aregs {
		s += number
	}
	return s
}

func ReadFile(strFileName string)(string, error){
	f, err := os.Open(strFileName)
	if err != nil {
		fmt.Println(err)
		return "", err
	}
	defer f.Close()
	buf := make([]byte, 1024)
	var strContent string = ""
	for {
		n, _ := f.Read(buf)
		if n == 0 {
			break
		}
		strContent += string(buf[0:n])
	}
	return strContent, nil
}

func main(){
	q, r := divide(5,3)
	fmt.Println(q, ",", r)
	total := sum(1,2,3,4)
	fmt.Println(total)
	slice := []int{1,2,3,4,5,6,7,8,9}
	fmt.Println(sum(slice...))
	str, err := ReadFile("test.go")
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	fmt.Println(str)
}
