package com.bool.study.strategy;

import com.google.gson.Gson;

public class JsonParamParser<T> extends AbstractParamParser<T> implements ParamParser<T> {

    @Override
    T doParser(Object param, Class type) {
        System.out.println("json parser");

        Gson gson = new Gson();
        return (T) gson.fromJson(param.toString(), type);
    }
}
