CXX = g++
#CXXFLAGS = -Wall -Wextra -Werror -O3 -std=c++11 -stdlib=libc++
#CXXFLAGS = -Wall -Wextra -Werror -O3
CXXFLAGS = -Wall
INCLUDES = `pkg-config --cflags --libs opencv`
SRCS = vc.cpp
OBJS = vc.o

.PHONY: all

all:
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SRCS) -o cv

clean:
	rm -f cv $(OBJS)
	@echo "all cleaned up!"
