################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../src/crowdfilter.cc \
../src/lsd.cc \
../src/parser.cc \
../src/stringutils.cc 

OBJS += \
./src/crowdfilter.o \
./src/lsd.o \
./src/parser.o \
./src/stringutils.o 

CC_DEPS += \
./src/crowdfilter.d \
./src/lsd.d \
./src/parser.d \
./src/stringutils.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cc
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


