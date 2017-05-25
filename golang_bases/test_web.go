package main

import (
	"net/http"
	"fmt"
)

type Handler interface {
	ServeHTTP(ResponseWriter, r *http.Request)
}

type HttpHandler struct {

}

func (this *HttpHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {

}

func HandleRequest(w http.ResponseWriter, r *http.Request)  {
	w.Header().Add("Content-Type", "	text/html;charset=utf-8")
	if r.Method == "POST" {
		r.ParseForm()
		w.Write([]byte("username: " + r.FormValue("username") + "<br/>"))
		w.Write([]byte("<hr/>"))
		names := r.Form["username"]
		w.Write([]byte("username has two: " + fmt.Sprintf("%v", names)))
		w.Write([]byte("<hr/>r.Form's content: " + fmt.Sprintf("%v", r.Form)))
		w.Write([]byte("<hr/>r.PostForm's content: " + fmt.Sprintf("%v", r.Form)))
	} else {
		strBody := `<form action="` + r.URL.RequestURI() + `"method="post">username:<input name="username" type="text" /><br />
		<input id="submit" type="submit" value="submit" /></form>`
		w.Write([]byte(strBody))
		r.ParseForm()
	}

}

func main()  {
	http.HandleFunc("/test", HandleRequest)
	http.ListenAndServe(":8888", nil)
}

