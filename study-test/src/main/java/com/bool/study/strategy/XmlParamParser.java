package com.bool.study.strategy;

import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;

import java.lang.reflect.Field;
import java.util.Iterator;

public class XmlParamParser<T> extends AbstractParamParser<T> implements ParamParser<T> {

    @Override
    T doParser(Object param, Class type) {
        Document doc;
        Object obj = null;
        try {
            doc = DocumentHelper.parseText(param.toString());
            Element root = doc.getRootElement();
            Iterator items = root.elementIterator();
            obj = type.newInstance();

            while (items.hasNext()) {
                Element item = (Element) items.next();
                String text = root.elementText(item.getName());
                Field field = type.getDeclaredField(item.getName());
                field.setAccessible(true);
                field.set(obj, text);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return (T) obj;
    }

    @Override
    void subCheckParam(Object param) {

        System.out.println("param = [" + param + "], type = [xml]");
    }
}
