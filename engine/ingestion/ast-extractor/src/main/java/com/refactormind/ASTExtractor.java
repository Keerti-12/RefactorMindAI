package com.refactormind;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class ASTExtractor {

    static class ClassData {
        String className;
        List<FieldData> fields = new ArrayList<>();
        List<MethodData> methods = new ArrayList<>();

        public ClassData(String className) {
            this.className = className;
        }
    }

    static class FieldData {
        String fieldName;
        String fieldType;

        public FieldData(String fieldName, String fieldType) {
            this.fieldName = fieldName;
            this.fieldType = fieldType;
        }
    }

    static class MethodData {
        String methodName;
        String returnType;
        String methodBody;

        public MethodData(String methodName, String returnType, String methodBody) {
            this.methodName = methodName;
            this.returnType = returnType;
            this.methodBody = methodBody;
        }
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Error: No file path provided.");
            System.exit(1);
        }

        try {
            CompilationUnit cu = StaticJavaParser.parse(new File(args[0]));
            List<ClassData> projectClasses = new ArrayList<>();

            for (ClassOrInterfaceDeclaration c : cu.findAll(ClassOrInterfaceDeclaration.class)) {

                ClassData classData = new ClassData(c.getNameAsString());

                for (FieldDeclaration field : c.findAll(FieldDeclaration.class)) {
                    String name = field.getVariables().get(0).getNameAsString();
                    String type = field.getElementType().asString();

                    classData.fields.add(new FieldData(name, type));
                }

                for (MethodDeclaration method : c.findAll(MethodDeclaration.class)) {
                    String name = method.getNameAsString();
                    String type = method.getTypeAsString();
                    String body = method.getBody().isPresent() ? method.getBody().get().toString() : "";

                    classData.methods.add(new MethodData(name, type, body));
                }

                projectClasses.add(classData);
            }

            Gson gson = new GsonBuilder().setPrettyPrinting().create();

            String jsonOutput = gson.toJson(projectClasses);

            System.out.println(jsonOutput);

        } catch (Exception e) {
            System.err.println("Failed to parse Java file: " + e.getMessage());
            System.exit(1);
        }
    }
}