# Documentación del Proyecto: Sistema de Validación de Diseño

## Descripción General
El sistema de validación de diseño permite realizar una serie de pruebas a los controles asignados a un auditor. El proceso incluye responder preguntas de diseño, proporcionar explicaciones y guardar las respuestas en la base de datos. Además, el sistema realiza un seguimiento del estado de las pruebas, calculando automáticamente el puntaje y cambiando el estado de los controles según las respuestas.

## Endpoint de entrada en desarrollo local
[http://localhost:8000/audit/login/](http://localhost:8000/audit/login/)

## Modelos
Los modelos principales de la aplicación incluyen:

### Control
Representa un control que será evaluado. Tiene los siguientes campos:

- `name`: Nombre del control.
- `description`: Descripción opcional del control.
- `assigned_auditor`: Usuario asignado al control (auditor).
- `cycle`: Ciclo al que pertenece el control.
- `date_elaborated`: Fecha en la que se elaboró el control.
- `status`: Estado del control (por ejemplo, "Sin iniciar", "En proceso", "Terminado").
- `total_hours`: Total de horas invertidas en el control.
- `consulted_resources`: Recursos consultados durante la evaluación.

### Validation
Representa la validación de un control. Tiene los siguientes campos:

- `control`: El control al que pertenece la validación.
- `design_score`: Puntaje obtenido en la validación del diseño.
- `status`: Estado de la validación (por ejemplo, "En proceso", "Terminado", "No evaluado").
- `date_elaborated`: Fecha en la que se elaboró la validación.
- `person_name`: Nombre de la persona que realizó la prueba.
- `person_role`: Cargo de la persona que realizó la prueba.

### DesignQuestion
Pregunta de diseño asociada a un control. Tiene los siguientes campos:

- `control`: El control al que pertenece la pregunta.
- `is_required`: Indica si la pregunta es obligatoria.
- `question`: El texto de la pregunta.

### DesignAnswer
Respuesta a una pregunta de diseño. Tiene los siguientes campos:

- `question`: La pregunta asociada a la respuesta.
- `answer`: La respuesta (Sí, No, No Aplica).
- `explanation`: Explicación adicional a la respuesta.

## Vistas

### control_design
Vista principal para gestionar las respuestas de la "Prueba de Diseño". Muestra las preguntas del control, permite seleccionar respuestas y agregar explicaciones. Al guardar las respuestas, también se actualiza la validación correspondiente del control.

**Flujo de trabajo:**

1. Se obtienen las preguntas asociadas al control.
2. Se muestran las respuestas existentes si ya han sido proporcionadas.
3. El usuario selecciona una respuesta y proporciona una explicación.
4. Al enviar el formulario, las respuestas se guardan y se actualiza la validación.

```python
@login_required
def control_design(request, control_id):
    control = get_object_or_404(Control, pk=control_id)
    questions = control.questions.all()
    existing_answers = DesignAnswer.objects.filter(question__control=control)
    validation = Validation.objects.filter(control=control).first()

    if request.method == 'POST':
        # Recoger y guardar las respuestas
        for question in questions:
            response = request.POST.get(f'response_{question.id}')
            explanation = request.POST.get(f'explanation_{question.id}')

            # Crear o actualizar las respuestas
            design_answer, created = DesignAnswer.objects.update_or_create(
                question=question,
                defaults={'answer': response, 'explanation': explanation},
            )
        
        # Actualizar la validación
        validation, validation_created = Validation.objects.update_or_create(
            control=control,
            defaults={
                'date_elaborated': request.POST.get('date_elaborated'),
                'person_name': request.POST.get('person_name'),
                'person_role': request.POST.get('person_role'),
            },
        )

        return redirect('dashboard')  # Redirigir después de guardar

    return render(request, 'audit/control_design.html', {
        'control': control,
        'questions': questions,
        'existing_answers': existing_answers,
        'validation': validation,
    })
```

## Plantillas
- Formulario de Respuestas (control_design.html)
- El formulario para registrar las respuestas de la prueba de diseño tiene tres secciones principales:

## Información del Control: Muestra el nombre y la descripción del control.
- Datos de Validación: Permite ingresar la fecha de ejecución de la prueba, el nombre de la persona que hizo la prueba y su cargo.
- Preguntas de Diseño: Muestra una tabla con las preguntas, un dropdown para seleccionar la respuesta (Sí, No, No Aplica) y un campo para agregar una explicación.

## Consideraciones Adicionales
- Cálculo del Estado del Control: Si todas las preguntas son respondidas y la validación es positiva (puntaje == 100), el estado del control se actualizará a "Terminado".
- Validación del Puntaje: El puntaje de la validación se calcula en función de las respuestas y se utiliza para actualizar el estado del control (por ejemplo, "Satisfactorio" si todas las respuestas son positivas).