tuvi\_mcp package
==================

The top-level package exports these public types, documented in dedicated pages:

* :doc:`Horoscope <horoscope>` — main user-facing class with ``from_birth()``, ``chart()``, ``transit()``, ``auspicious()``, and ``render_chart()``
* :doc:`BirthInfo <horoscope>` — immutable birth input dataclass
* :doc:`Gender <enums>` — ``MALE`` / ``FEMALE`` enum
* :doc:`Calendar <enums>` — ``SOLAR`` / ``LUNAR`` enum
* :doc:`HoroscopeResult <results>` — chart result with ``thien_ban``, ``dia_ban``, ``cach_cuc``
* :doc:`TransitResult <results>` — transit (Vận Hạn) analysis result
* :doc:`AuspiciousResult <results>` — auspicious day evaluation result
