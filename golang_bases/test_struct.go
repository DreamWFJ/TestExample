package main

import "fmt"

type Student struct {
	Name string
	Age int
	class string
}

func test_1()  {
	s1 := new(Student)
	s1.Name = "汪方杰"
	s1.Age = 27
	s1.class = "中级十班"
	fmt.Println(s1)
}

func test_2()  {
	s1 := Student{"张三", 12, "3班"}
	fmt.Println(s1)
}

func test_3()  {
	s1 := Student{Name:"小王", Age:34, class:"90班"}
	fmt.Println(s1)
	fmt.Println(s1.getAge(), s1.getName())
}

func (this Student) getName() string {
	return this.Name
}

func (this *Student) getAge()int {
	return this.Age
}

func (this *Student) Display() {
	fmt.Println(this.Name, ",", this.Age)
}

type CollegeStudent struct {
	Student
	Profession string
}

func (this *CollegeStudent) Display() {
	fmt.Println(this.Name, ",", this.Profession, ",", this.Age, ",", this.class)
}
func test_4()  {
	fmt.Println("into test_4")
	s1 := CollegeStudent{Student:Student{Name:"李四", Age:24, class:"2004(2)班"},Profession:"物理"}
	s1.Display()
	fmt.Println(s1.Student.Name)
	fmt.Println(s1.Name)
}
func main()  {
	test_1()
	test_2()
	test_3()
	test_4()
}
