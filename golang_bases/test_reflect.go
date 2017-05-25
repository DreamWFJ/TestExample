package main

import (
	"fmt"
	"reflect"
	"encoding/xml"
)

type StudentD struct {
	Name string "学生姓名"
	Age int `a:"1111"b:"22222"`
}

type StudentE struct {
	XMLName xml.Name `xml:"student"`
	Name string `xml:"name"`
	Age int `xml:"age"`
}

func (this *StudentD) PrintName() {
	fmt.Println(this.Name)
}

func (this *StudentD) GetAge() int {
	return this.Age
}

func test_reflect_1()  {
	s := StudentD{Name:"abc", Age:19}
	//反射键的信息
	rt := reflect.TypeOf(s)
	//反射值的信息
	rv := reflect.ValueOf(s)
	if rt.Kind() == reflect.Ptr {
		rt = rt.Elem()
	}
	if rv.Kind() == reflect.Ptr {
		rv = rv.Elem()
	}
	//输出类型所在的包的路径
	fmt.Println(rt.PkgPath())
	//反射取所有字段
	fmt.Println(rt.Name(), "total", rt.NumField(), "field")
	for i, j := 0, rt.NumField(); i < j; i++ {
		rtField := rt.Field(i)
		rvField := rv.FieldByName(rtField.Name)
		fmt.Println(rtField.Name, "=",rvField)
		fmt.Println()
	}
	rt = reflect.PtrTo(rt)
	fmt.Println(rt.Name(), "total", rt.NumMethod(), "method")
	for i, j := 0, rt.NumMethod(); i < j; i++ {
		mt := rt.Method(i)
		fmt.Println(mt.Name)
		numIn := mt.Type.NumIn()
		numOut := mt.Type.NumOut()

		if numIn > 0 {
			fmt.Println("\tTotal", numIn, "in args")
			for k := 0; k < numIn; k++ {
				in := mt.Type.In(k)
				fmt.Println("\t", in.Name(), "\t", in.Kind())
			}

		}
		if numOut > 0 {
			fmt.Println("\tTotal", numOut, "out args")
			for k := 0; k < numOut; k++ {
				out := mt.Type.Out(k)
				fmt.Println("\t", out.Name(), "\t", out.Kind())
			}

		}
	}
}

func ShowSlice(s []reflect.Value)  {
	if s != nil && len(s) > 0 {
		for _, v := range s {
			fmt.Println(v.Interface())
		}
	}
}
func test_reflect_2()  {
	s := StudentD{Name:"abc", Age:19}
	rt := reflect.TypeOf(&s)
	rv := reflect.ValueOf(&s)
	fmt.Println("typeof call function")
	rtm, ok := rt.MethodByName("PrintName")
	if ok {
		var parm []reflect.Value
		parm = append(parm, rv)
		rtm.Func.Call(parm)
	}
	fmt.Println("valueof call function")
	rvm := rv.MethodByName("GetAge")
	ret := rvm.Call(nil)
	fmt.Println("return value")
	ShowSlice(ret)
}

func test_reflect_3()  {
	s := StudentD{}
	rt := reflect.TypeOf(s)
	if fieldName, ok := rt.FieldByName("Name"); ok {
		fmt.Println(fieldName.Tag)
	}
	if fieldName, ok := rt.FieldByName("Age"); ok {
		fmt.Println(fieldName.Tag.Get("a"))
		fmt.Println(fieldName.Tag.Get("b"))
	}
}
func main()  {
	//test_reflect_1()
	//test_reflect_2()
	test_reflect_3()
}