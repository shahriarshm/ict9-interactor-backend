# Interactor

This project is written for 9th round of [Sharif ICT Challenge](https://sharifict.ir/). Our team won the second place. So we shared our project with public to help others learn more about the competition and our project.

This project is a widget management system implemented as a microservice architecture. It provides APIs to create, read, update, and delete widgets. The project is structured into several modules, each responsible for different aspects of the application, and is distributed across three GitLab repositories.

## Challenge

To understand the challenge and our solution, you can read the [Persian Version](./docs/ict-challenge-fa.md) or [English Version](./docs/ict-challenge-en.md) of the challenge.

# Project Microservices

- [Interactor Backend](https://github.com/shahriarshm/ict9-interactor-backend.git)
- [Interactor Frontend](https://github.com/MSNP1381/ICT9-interactor-campaigns.git)
- [Interactor Widget Service](https://github.com/shahriarshm/ict9-interactor-widget-service.git)

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
    git clone https://github.com/shahriarshm/ict9-interactor-backend.git
    git clone https://github.com/MSNP1381/ICT9-interactor-campaigns.git
    git clone https://github.com/shahriarshm/ict9-interactor-widget-service.git
    ```
2. Navigate to each project directory and follow the specific installation instructions in their respective README files.

3. Run using docker:
    ```sh
    docker compose up -d
    ```

## Usage

To run the application, use the following command in each project directory:
