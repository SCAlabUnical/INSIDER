# Edge Cloud Continuum Workflow Designer (ECCD)

Deployed at: https://aleandropresta.github.io/ecc-workflow-designer/

## Table of Contents

1. [Introduction](#introduction)
    - [Workflows](#workflows)

## Introduction

ECCD is a Web Based Workflow Designer that allows the user to create Workflows composed of Abstract Services.

### Workflows

A workflow is a is a an undirected graph, composed by nodes and edges. Each node rappresents an Abstract Service. Services can be of 4 types:

-   **Computation** (green);
-   **Communication** (blue);
-   **Storage** (yellow);

In the workflow are also rapresented the **Devices** (white). The workflow inside the application uses the json format. Each node is an element of the `nodes` object, each edge an element of the `connections` object (connecting two nodes using their IDs):

```json
{
    "nodes": [
        {
            "name": "Device",
            "id": 0,
            "type": "Device",
            "description": "Example device",
            "x": 26,
            "y": 27,
            "width": 300,
            "height": 90,
            "quantity": 1,
            "parameters": [],
            "inputConnectors": [
                {
                    "name": "",
                    "direction": "x"
                },
                {
                    "name": "",
                    "direction": "y"
                }
            ],
            "outputConnectors": [
                {
                    "name": "",
                    "direction": "x"
                },
                {
                    "name": "",
                    "direction": "y"
                }
            ]
        },
        ...
    ],
    "connections": [
        {
            "name": "Connection 1",
            "source": {
                "nodeID": 0,
                "connectorIndex": 0
            },
            "dest": {
                "nodeID": 1,
                "connectorIndex": 0
            }
        },
        ...
    ]
}
```

There are two type of parametes inside a node object:

-   **Visual parameters** such as `x`, `y`, `width` and `height` that describe the position and the dimension of a node inside the UI;
-   **(?) Parameters**: define vital characteristics of the workflows such as the `parameters` (a list of constraints that must be satisfied), the `name`, the `ID` and the `quantity` (**TODO** refactor).

### Tecnologies Used

-   AngularJS;
-   JQuery;
-   Bootstrap.
