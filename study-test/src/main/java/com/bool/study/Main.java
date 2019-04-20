package com.bool.study;

import com.bool.study.strategy.JsonParamParser;
import com.bool.study.strategy.ParamParserHelper;
import com.bool.study.strategy.XmlParamParser;
import com.bool.study.strategy.beans.User;

import java.util.ArrayList;
import java.util.List;

public class Main {

	public static void main(String[] args) {

        ParamParserHelper<User> parserHelper = null;
        parserHelper = new ParamParserHelper<>(new XmlParamParser<>());
        User user = parserHelper.doParse("<user><name>张三</name></user>", User.class);

        parserHelper = new ParamParserHelper<>(new JsonParamParser<>());

        User user1 = parserHelper.doParse("{'name':'李四'}", User.class);

        List<String> list = new ArrayList<>();

        System.out.println(user1.getName());
	}

}
