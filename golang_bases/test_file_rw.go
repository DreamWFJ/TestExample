package main

import (
	"fmt"
	"path"
	"strings"
	"path/filepath"
	"os"
	"io"
	"io/ioutil"
)

func test_file_1()  {
	//返回路径的最后一部分
	fmt.Println(path.Base("/usr/bin"))
	fmt.Println(path.Base(""))
	fmt.Println(path.Base("C:\\Windows"))
	fmt.Println(path.Base(strings.Replace("C:\\Windows", "\\", "/", -1)))
}

func test_file_2()  {
	//获取等价路径
	fmt.Println(path.Clean("/a/b/../c"))
	fmt.Println(path.Clean("/a/b/../././c"))
}

func test_file_3()  {
	//获取目录部分
	fmt.Println(path.Dir("/a/b/../c/d/e"))
	fmt.Println(path.Clean("/a/b/"))
}
func test_file_4()  {
	//获取扩展
	fmt.Println(path.Ext("/a/b/../c/d./e"))
	fmt.Println(path.Ext("/a/b/test.txt"))
}

func test_file_5()  {
	//判断路径是否绝对路径
	fmt.Println(path.IsAbs("/a/b/c"))
	fmt.Println(path.IsAbs(strings.Replace("C:\\Windows\\system", "\\", "/", -1)))
}

func test_file_6()  {
	//路径拼接
	fmt.Println(path.Join("/a/b", "c"))
	fmt.Println(path.Join("C:\\Windows", "System"))
}

func test_file_7()  {
	//路径分割
	fmt.Println(path.Split("/a/b/test.txt"))
	fmt.Println(path.Split("/a/b/c"))
}

func test_file_8()  {
	//把相对路径转换为绝对路径
	fmt.Println(filepath.Abs("."))
}

func DispFile(path string, info os.FileInfo, err error) error {
	fmt.Println(path, "----------", info.Name(), "-----------", info.IsDir())
	return nil
}
func test_file_9()  {
	//遍历路径
	filepath.Walk("..", DispFile)
}

func test_file_10()  {
	//文件读写
	f, err := os.OpenFile("1.txt", os.O_RDONLY | os.O_APPEND | os.O_CREATE, 0666)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	f.WriteString("\r\n中国人民银行\r\n")
	buf := make([]byte, 1024)
	var str string
	//os.SEEK_SET  os.SEEK_CUR os.SEEK_END
	f.Seek(0, os.SEEK_SET)
	for {
		n, ferr := f.Read(buf)
		if ferr != nil && ferr != io.EOF {
			fmt.Println(ferr.Error())
			break
		}
		if n == 0 {
			break
		}
		fmt.Println(n)
		str += string(buf[0:n])
	}
	fmt.Println(str)
	f.Close()
}

func test_file_11()  {
	//文件读写
	f, err := os.OpenFile("1.txt", os.O_RDONLY | os.O_APPEND | os.O_CREATE, 0666)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	defer f.Close()
	buf, err1 := ioutil.ReadAll(f)
	if err1 != nil {
		fmt.Println(err1.Error())
		return
	}
	fmt.Println(string(buf))
}

func test_file_12()  {
	//文件读写
	buf, err := ioutil.ReadFile("1.txt")
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	fmt.Println(string(buf))
}

func test_file_13()  {
	//文件读写
	err := ioutil.WriteFile("1.txt", []byte("abcdefg"), 0777)
	if err != nil {
		fmt.Println(err.Error())
		return
	} else {
		fmt.Println("OK")
	}
}
func test_file_14()  {
	//文件读写
	f, err := os.OpenFile(".", os.O_RDONLY , 0666)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	arrFile, err1 := f.Readdir(0)
	if err1 != nil {
		fmt.Println(err1.Error())
		return
	}
	for k, v := range arrFile {
		fmt.Println(k, "\t", v.Name(), "\t", v.IsDir())
	}
}

func test_file_15()  {
	//文件读写
	arrFile, err1 := ioutil.ReadDir(".")
	if err1 != nil {
		fmt.Println(err1.Error())
		return
	}
	for k, v := range arrFile {
		fmt.Println(k, "\t", v.Name(), "\t", v.IsDir())
	}
}
func main()  {
	//test_file_1()
	//test_file_2()
	//test_file_3()
	//test_file_4()
	//test_file_5()
	//test_file_6()
	//test_file_7()
	//test_file_8()
	//test_file_9()
	//test_file_10()
	//test_file_11()
	//test_file_12()
	//test_file_13()
	//test_file_14()
	test_file_15()
}