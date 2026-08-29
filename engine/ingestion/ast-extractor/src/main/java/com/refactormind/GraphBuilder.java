package com.refactormind;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.ImportDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.body.ConstructorDeclaration;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.LinkedHashMap;

class GraphBuilder {
    public static class Node {
        String id;
        String type; // "FILE, CLASS, METHOD, FIELD"
        String name;
        String file;
        int line;

        public Node(String id, String type, String name, String file, int line) {
            this.id = id;
            this.type = type;
            this.name = name;
            this.file = file;
            this.line = line;
        }
    }

    public static class Edge {
        String from;
        String to;
        String type; // "CONTAINS, DEPENDS_ON, CALLS"

        public Edge(String from, String to, String type) {
            this.from = from;
            this.to = to;
            this.type = type;
        }
    }

    public static class Graph {
        List<Node> nodes = new ArrayList<>();
        List<Edge> edges = new ArrayList<>();

        public void addNode(Node node) {
            nodes.add(node);
        }

        public void addEdge(Edge edge) {
            edges.add(edge);
        }
    }

    public static List<File> findJavaFiles(File dir) {
        List<File> files = new ArrayList<>();
        if (!dir.exists() || !dir.isDirectory())
            return files;

        File[] entries = dir.listFiles();
        if (entries == null)
            return files;

        for (File file : entries) {
            if (file.isDirectory()) {
                files.addAll(findJavaFiles(file));
            } else if (file.getName().endsWith(".java")) {
                files.add(file);
            }
        }
        return files;
    }

    private static void processFields(ClassOrInterfaceDeclaration c, String className, String fileName, Graph graph,
            Map<String, String> typeMap) {
        for (FieldDeclaration field : c.findAll(FieldDeclaration.class)) {
            String fieldType = field.getElementType().asString();

            for (VariableDeclarator var : field.getVariables()) {
                String fieldName = var.getNameAsString();
                String fieldId = className + "." + fieldName;
                int fieldLine = field.getBegin().map(p -> p.line).orElse(0);

                graph.addNode(new Node(fieldId, "FIELD", fieldName, fileName, fieldLine));

                graph.addEdge(new Edge(className, fieldId, "CONTAINS"));

                if (typeMap.containsKey(fieldType)) {
                    graph.addEdge(new Edge(className, typeMap.get(fieldType), "DEPENDS_ON"));
                }
            }
        }

    }

    private static void processMethods(ClassOrInterfaceDeclaration c, String className, String fileName, Graph graph,
            Map<String, String> typeMap) {
        Map<String, String> fieldTypes = new HashMap<>();
        for (FieldDeclaration field : c.findAll(FieldDeclaration.class)) {
            String type = field.getElementType().asString();
            for (VariableDeclarator var : field.getVariables()) {
                fieldTypes.put(var.getNameAsString(), type);
            }
        }

        for (ConstructorDeclaration constructor : c.findAll(ConstructorDeclaration.class)) {
            String constructorName = constructor.getNameAsString();

            List<String> paramTypes = new ArrayList<>();
            for (Parameter params : constructor.getParameters()) {
                paramTypes.add(params.getTypeAsString());
            }

            String constructorId = className + "." + constructorName + "(" + String.join(",", paramTypes) + ")";
            int constructorLine = constructor.getBegin().map(p -> p.line).orElse(0);

            graph.addNode(new Node(constructorId, "CONSTRUCTOR", constructorName, fileName, constructorLine));

            graph.addEdge(new Edge(className, constructorId, "CONTAINS"));

            constructor.findAll(MethodCallExpr.class).forEach(call -> {
                String calledMethod = call.getNameAsString();

                call.getScope().ifPresent(scope -> {
                    String scopeName = scope.toString();
                    String targetClass = fieldTypes.getOrDefault(scopeName, null);

                    String argSuffix;

                    if (call.getArguments().isEmpty()) {
                        argSuffix = "()";
                    } else {
                        argSuffix = "";
                    }

                    if (targetClass != null && typeMap.containsKey(targetClass)) {
                        String targetMethodId = targetClass + "." + calledMethod + argSuffix;
                        graph.addEdge(new Edge(constructorId, targetMethodId, "CALLS"));
                    }
                });
            });
        }

        for (MethodDeclaration method : c.findAll(MethodDeclaration.class)) {
            String methodName = method.getNameAsString();

            List<String> paramTypes = new ArrayList<>();
            for (Parameter param : method.getParameters()) {
                paramTypes.add(param.getTypeAsString());
            }

            String methodId = className + "." + methodName + "(" + String.join(",", paramTypes) + ")";
            int methodLine = method.getBegin().map(p -> p.line).orElse(0);

            graph.addNode(new Node(methodId, "METHOD", methodName, fileName, methodLine));

            graph.addEdge(new Edge(className, methodId, "CONTAINS"));

            method.findAll(MethodCallExpr.class).forEach(call -> {
                String calledMethod = call.getNameAsString();

                String argSuffix;
                if (call.getArguments().isEmpty()) {
                    argSuffix = "()";
                } else {
                    argSuffix = "";
                }

                call.getScope().ifPresent(scope -> {
                    String scopeName = scope.toString();

                    String targetClass = fieldTypes.getOrDefault(scopeName, null);

                    if (targetClass != null && typeMap.containsKey(targetClass)) {
                        String targetMethodId = targetClass + "." + calledMethod + argSuffix;
                        graph.addEdge(new Edge(methodId, targetMethodId, "CALLS"));
                    }
                });
            });
        }
    }

    private static void processFile(File file, CompilationUnit cu, Graph graph, Map<String, String> typeMap) {
        String fileName = file.getName();

        String fileId = fileName;
        graph.addNode(new Node(fileId, "FILE", fileName, "", 0));

        for (ClassOrInterfaceDeclaration c : cu.findAll(ClassOrInterfaceDeclaration.class)) {
            String className = c.getNameAsString();
            String classId = className;
            int classLine = c.getBegin().map(p -> p.line).orElse(0);

            graph.addNode(new Node(classId, "CLASS", className, fileName, classLine));

            graph.addEdge(new Edge(fileId, classId, "CONTAINS"));

            processFields(c, className, fileName, graph, typeMap);

            processMethods(c, className, fileName, graph, typeMap);
        }

        cu.findAll(ImportDeclaration.class).forEach(imp -> {
            String importedName = imp.getNameAsString();
            String simpleName = importedName.substring(importedName.lastIndexOf('.') + 1);

            if (typeMap.containsKey(simpleName)) {
                graph.addEdge(new Edge(fileName, simpleName, "IMPORTS"));
            }
        });
    }

    public static Graph buildGraph(String directoryPath) throws Exception {
        Graph graph = new Graph();

        List<File> javaFiles = findJavaFiles(new File(directoryPath));

        Map<String, String> typeMap = new HashMap<>();
        Map<File, CompilationUnit> parsedFiles = new LinkedHashMap<>();

        for (File file : javaFiles) {
            CompilationUnit cu = StaticJavaParser.parse(file);
            parsedFiles.put(file, cu);

            cu.findAll(ClassOrInterfaceDeclaration.class).forEach(c -> {
                typeMap.put(c.getNameAsString(), c.getNameAsString());
            });
        }

        for (Map.Entry<File, CompilationUnit> entry : parsedFiles.entrySet()) {
            processFile(entry.getKey(), entry.getValue(), graph, typeMap);
        }
        return graph;
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("Usage: GraphBuilder <directory-path>");
            System.exit(1);
        }

        Graph graph = buildGraph(args[0]);

        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        System.out.println(gson.toJson(graph));
    }
}
