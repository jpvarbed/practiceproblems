package practice

import (
	"strings"
)

func NoSpace(word string) string {
	return strings.Replace(word, " ", "", -1)
}

func Summation(n int) int {
	sum := 0
	for i := 1; i < (n + 1); i++ {
		sum += i
	}
	return sum
}
