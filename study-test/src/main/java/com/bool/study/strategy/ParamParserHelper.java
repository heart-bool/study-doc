package com.bool.study.strategy;

public class ParamParserHelper<T> {

    private ParamParser<T> paramParser;

    public ParamParserHelper(ParamParser<T> paramParser) {
        this.paramParser = paramParser;
    }

    public T doParse(Object p, Class t) {
        return paramParser.parse(p, t);
    }

}
