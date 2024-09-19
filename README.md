# Interactor

This project is a widget management system implemented as a microservice architecture. It provides APIs to create, read, update, and delete widgets. The project is structured into several modules, each responsible for different aspects of the application, and is distributed across three GitLab repositories.

- [Interactor Backend](http://git.sharifict.ir/shahriarshm/interactor-backend.git)
- [Interactor Frontend](http://git.sharifict.ir/shahriarshm/interactor-frontend.git)
- [Interactor Widget Service](http://git.sharifict.ir/shahriarshm/interactor-widget-service.git)

## Architecture

![Interactor](./assets/interactor.png)

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

The widget management system is designed to manage widgets efficiently. It includes the following modules:

- **API**: Handles the HTTP requests and responses.
- **Models**: Defines the data structures.
- **Services**: Contains the business logic.
- **CRUD**: Handles the database operations.
- **Config**: Manages the configuration settings.

## Installation

To install the project, follow these steps:

1. Clone the repositories:
    ```sh
    git clone http://git.sharifict.ir/shahriarshm/interactor-backend.git
    git clone http://git.sharifict.ir/shahriarshm/interactor-frontend.git
    git clone http://git.sharifict.ir/shahriarshm/interactor-widget-service.git
    ```
2. Navigate to each project directory and follow the specific installation instructions in their respective README files.

3. Run using docker:
    ```sh
    docker compose up -d
    ```

## Usage

To run the application, use the following command in each project directory:
