package main

import (
	"fmt"
	"time"
)

var maxprime = 2000000

func make_primes(ch chan int) {
	// The Sieve of Eratosthenes.
	// If sieve[i] is true, it is a composite number
	sieve := make([]bool, maxprime+1)
	for i := 2; i < maxprime; i++ {
		if !sieve[i] {
			// A new prime!
			ch <- i
			for j := i * 2; j < maxprime; j += i {
				sieve[j] = true
			}
		}
	}
	close(ch)
}

func main() {
	pchan := make(chan int)
	t := time.Now()
	go make_primes(pchan)
	sum := 0
	for p := range pchan {
		sum += p
	}
	fmt.Println(sum)
	fmt.Println("runtime:", time.Since(t))
}
