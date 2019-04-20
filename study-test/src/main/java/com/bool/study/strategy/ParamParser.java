package com.bool.study.strategy;

public interface ParamParser<T> {

    T parse(Object param, Class type);

}
