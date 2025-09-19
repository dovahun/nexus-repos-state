package src

import (
	"bytes"
	"github.com/tidwall/gjson"
	"io"
	"log/slog"
	"net/http"
	"os"
)

func SendRequest(url string, reqMethod string, requestBody string, nexusUser string, nexusUserPassword string) string {
	reqBody := bytes.NewBufferString(requestBody)
	logger := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))

	req, err := http.NewRequest(reqMethod, url, reqBody)
	if err != nil {
		panic(err)
	}
	req.Header.Set("Content-Type", "application/json")

	// авторизация Basic
	req.SetBasicAuth(nexusUser, nexusUserPassword)

	// выполняем запрос через клиент
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	// добавить обработчик статусов кода
	logger.Info(reqMethod + " request status is " + resp.Status + "" + gjson.Get(string(body), "message").String() + " " + url)
	defer resp.Body.Close()

	return string(body)
}

func GetRequest(url string, requestPath string, nexusUser string, nexusUserPassword string) string {
	requestBody := ""
	fullUrl := url + requestPath

	return SendRequest(fullUrl, "GET", requestBody, nexusUser, nexusUserPassword)
}

func PostRequest(url string, requestPath string, requestBody string, nexusUser string, nexusUserPassword string) string {
	fullUrl := url + requestPath

	return SendRequest(fullUrl, "POST", requestBody, nexusUser, nexusUserPassword)
}
func PutRequest(url string, objName string, requestPath string, requestBody string, nexusUser string, nexusUserPassword string) string {
	fullUrl := url + requestPath + "/" + objName

	return SendRequest(fullUrl, "PUT", requestBody, nexusUser, nexusUserPassword)
}
