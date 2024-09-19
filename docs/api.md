# API Documentation

## Endpoints

### Widget Templates

- **GET /widget-templates**: Retrieve a list of widget templates.
- **POST /widget-templates**: Create a new widget template.

### Widgets

- **GET /widgets**: Retrieve a list of widgets.
- **POST /widgets**: Create a new widget.
- **GET /widgets/{id}**: Retrieve a widget by ID.
- **PUT /widgets/{id}**: Update a widget by ID.
- **DELETE /widgets/{id}**: Delete a widget by ID.

## Files

- `app/api/widget_templates.py`: Handles widget template endpoints.
- `app/api/widgets.py`: Handles widget endpoints.