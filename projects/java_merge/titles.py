"""Inline display names used when one post links to another.

The old posts referred to each other as "post 14", which was fine in a 29-post
track and is wrong the moment the track becomes 64 and gains sections. Numbers
are also silently wrong rather than visibly broken — a link still works, it just
misleads. These names replace them, and they do not rot when the order changes.
"""

INLINE = {
    "java-get-started": "Get Started",
    "introduction-to-java": "Introduction to Java",
    "java-variables": "Variables",
    "java-data-types": "Data Types",
    "java-operators": "Operators",
    "java-string": "String",
    "java-conditional-statements": "Conditional Statements",
    "java-for-loop": "Loops",
    "java-arrays": "Arrays",
    "java-method": "Methods",
    "java-class": "Classes",
    "java-oop": "OOP",
    "java-interface": "Interfaces",
    "java-static-and-final-keywords": "static and final",
    "java-packages": "Packages",
    "java-collections": "Collections",
    "java-exception-handling": "Exception Handling",
    "java-debugging": "Debugging",
    "how-to-solve-java-problems": "How to Solve Java Problems",
    "java-best-practices": "Best Practices",
    "java-code-snippets": "Code Snippets",
    # the incoming posts that now own these topics
    "java-8-lambda-expression": "Lambda Expressions",
    "java-8-functional-interfaces": "Functional Interfaces",
    "java-8-method-references": "Method References",
    "java-8-streams": "Streams",
    "java-8-collectors-class": "Collectors",
    "java-8-optional": "Optional",
    "java-8-foreach": "forEach",
    "java-8-date-time-api": "the Date and Time API",
    "java-8-completablefuture": "CompletableFuture",
    "java-8-interface-default-methods-and-static-methods": "default and static interface methods",
    "java-17-records": "Records",
    "java-17-sealed-classes": "Sealed Classes",
    "java-17-switch-expressions": "Switch Expressions",
    "java-17-text-blocks": "Text Blocks",
    "java-11-string-methods": "the Java 11 String methods",
    "java-21-virtual-threads": "Virtual Threads",
    "java-21-sequenced-collections": "Sequenced Collections",
    "java-advanced-generics": "Generics",
    "java-advanced-multithreading": "Multithreading",
    "java-advanced-regex": "Regex",
}
