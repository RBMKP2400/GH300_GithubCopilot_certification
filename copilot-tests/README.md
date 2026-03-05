# GH-300 — Simulacros de examen (copilot-tests)

Módulo de práctica teórica para la certificación GH-300, con dos simulacros completos, clave de respuestas, explicaciones y generación automática de reporte.

---

## Qué incluye

- 2 tests de práctica:
  - `copilot_test_1_questions.md`
  - `copilot_test_2_questions.md`
- Banco de respuestas y explicaciones en `docs/`
- Script de evaluación: `generate_report.py`
- Reporte final por dominio con estado PASS/FAIL

---

## Flujo de uso recomendado

1. Abre un archivo de preguntas y responde marcando opciones:
   - cambia `#### [ ]` por `#### [x]`
2. Guarda el archivo.
3. Ejecuta el generador de reporte.
4. Revisa aciertos/errores por dominio y repasa explicaciones.

> Recomendación de simulación real: completar cada test en 100 minutos.

---

## Comandos

Desde la carpeta `copilot-tests/`:

```bash
python generate_report.py 1
python generate_report.py 2
```

También puede ejecutarse desde la raíz del repositorio:

```bash
python copilot-tests/generate_report.py 1
python copilot-tests/generate_report.py 2
```

---

## Salida generada

Para cada test se crea:

- `copilot_test_1_report.md` o `copilot_test_2_report.md` (en `copilot-tests/`)

El reporte contiene:

- Resumen global (respondidas, no respondidas, correctas, incorrectas)
- Porcentaje final y resultado PASS/FAIL
- Desglose por dominio
- Preguntas incorrectas/no respondidas por dominio
- Sección final con explicaciones completas

---

## Criterio de aprobación

- PASS: 36 o más respuestas correctas (≥ 72%)
- FAIL: menos de 36 respuestas correctas

---

## Estructura de archivos

- Preguntas: `copilot_test_X_questions.md`
- Respuestas: `docs/copilot_test_X_answers.md`
- Explicaciones: `docs/copilot_test_X_explanations.md`
- Reporte generado: `copilot_test_X_report.md`

---

## Notas útiles

- Se acepta `x` o `X` en los checkboxes.
- Las preguntas multi-select requieren marcar todas las opciones correctas.
- Si hay diferencias entre archivos de preguntas/respuestas, el script añade diagnósticos en el reporte.

