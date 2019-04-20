package com.bool.study.strategy;

public abstract class AbstractParamParser<T> implements ParamParser<T> {

    @Override
    public T parse(Object param, Class type) {
        checkParam(param);
        return doParser(param, type);
    }

    void checkParam(Object param) {
        if (param == null) {
            throw new NullPointerException("Param is not null");
        }

        subCheckParam(param);
    }

    void subCheckParam(Object param) {}

    abstract T doParser(Object param, Class type);

}
