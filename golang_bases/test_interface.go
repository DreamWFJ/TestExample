package main

import "fmt"

type StudentA struct {
	Name string
	Age int
	Class string
}

type ISstudentA interface {
	GetName() string
	GetAge() int
}

func (this *StudentA) GetName() string {
	return this.Name
}

func (this *StudentA) GetAge() int {
	return this.Age
}

func main()  {
	var s1 ISstudentA = &StudentA{"李四", 23, "2004(2)班"}
	fmt.Println(s1.GetName(), ", ", s1.GetAge())
}