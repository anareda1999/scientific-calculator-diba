"""
ui/i18n.py
==========
Translation tables for English / Français / العربية.
"""

__all__ = ["STRINGS", "LANGUAGES", "translate"]

LANGUAGES = [("fr", "Français"), ("en", "English"), ("ar", "العربية")]

# key -> {en, fr, ar}
STRINGS = {
    # ── App ───────────────────────────────────────────────────────
    "app_title": {"en": "Scientific Calculator", "fr": "Calculatrice Scientifique",
                  "ar": "الآلة الحاسبة العلمية"},
    "language":  {"en": "Language", "fr": "Langue", "ar": "اللغة"},
    "scientific":{"en": "SCIENTIFIC", "fr": "SCIENTIFIQUE", "ar": "علمي"},
    "copyright": {"en": "© reda anagou", "fr": "© reda anagou", "ar": "© reda anagou"},

    # ── Windows / modules ────────────────────────────────────────
    "converter":     {"en": "Converter", "fr": "Convertisseur", "ar": "محول الوحدات"},
    "equations":     {"en": "Equations", "fr": "Équations", "ar": "المعادلات"},
    "grapher":       {"en": "Graphing", "fr": "Graphique", "ar": "الرسوم البيانية"},
    "formulas":      {"en": "Formulas", "fr": "Formules", "ar": "الصيغ"},
    "matrices":      {"en": "Matrices", "fr": "Matrices", "ar": "المصفوفات"},
    "calculus":      {"en": "Calculus", "fr": "Calcul", "ar": "التفاضل والتكامل"},
    "statistics":    {"en": "Statistics", "fr": "Statistiques", "ar": "الإحصاء"},
    "advanced":      {"en": "Advanced", "fr": "Analyse", "ar": "تحليل متقدم"},
    "history":       {"en": "History", "fr": "Historique", "ar": "السجل"},

    # ── Advanced analysis ─────────────────────────────────────────
    "advanced_title":   {"en": "Advanced Analysis", "fr": "Analyse Avancee",
                         "ar": "تحليل متقدم"},
    "limit_point":      {"en": "Point approached (a, inf, -inf)",
                         "fr": "Point approche (a, inf, -inf)",
                         "ar": "النقطة المقاربة (a، inf، -inf)"},
    "limit_direction":  {"en": "Direction", "fr": "Direction",
                         "ar": "الاتجاه"},
    "lim_both":   {"en": "Two-sided", "fr": "Double sens", "ar": "من الجانبين"},
    "lim_right":  {"en": "From the right", "fr": "Par la droite", "ar": "من اليمين"},
    "lim_left":   {"en": "From the left", "fr": "Par la gauche", "ar": "من اليسار"},
    "lim_result": {"en": "Limit", "fr": "Limite", "ar": "النهاية"},
    "taylor_point": {"en": "Expansion point (a)", "fr": "Point de developpement (a)",
                     "ar": "نقطة التوسع (a)"},
    "taylor_order": {"en": "Order of the expansion", "fr": "Ordre du developpement",
                     "ar": "رتبة التوسع"},
    "ineq_expression": {"en": "Expression f(x) to solve", "fr": "Expression f(x) a resoudre",
                         "ar": "التعابير f(x) المراد حلها"},
    "ineq_sign":   {"en": "Inequality", "fr": "Inequation", "ar": "المتراجحة"},
    "ineq_note":   {"en": "The solution is searched numerically inside the given interval.",
                    "fr": "La solution est recherchee numeriquement dans l'intervalle indique.",
                    "ar": "يتم البحث عن الحل عددياً داخل الفترة المحددة."},
    "ode_expression": {"en": "Right-hand side  (use y and yp)",
                        "fr": "Membre de droite  (utilisez y et yp)",
                        "ar": "الطرف الأيمن  (استخدم y و yp)"},
    "ode_order":   {"en": "Order of the equation", "fr": "Ordre de l'equation",
                    "ar": "رتبة المعادلة"},
    "ode_initial": {"en": "Initial conditions", "fr": "Conditions initiales",
                    "ar": "الشروط الابتدائية"},
    "ode_range":   {"en": "Resolution range", "fr": "Plage de resolution",
                    "ar": "مجال الحل"},
    "ode_result":  {"en": "Result", "fr": "Resultat", "ar": "النتيجة"},
    "ode_note":    {"en": "Runge-Kutta 4 method", "fr": "Methode de Runge-Kutta 4",
                    "ar": "طريقة رونج-كوتا 4"},

    # ── Calculator ────────────────────────────────────────────────
    "answer":        {"en": "Ans", "fr": "Ans", "ar": "ن"},
    "answer_label":  {"en": "Last answer", "fr": "Dernier résultat", "ar": "آخر نتيجة"},
    "history_empty": {"en": "No calculation yet", "fr": "Aucun calcul", "ar": "لا يوجد حساب"},
    "history_clear": {"en": "Clear history", "fr": "Effacer l'historique", "ar": "مسح السجل"},
    "error":         {"en": "Error", "fr": "Erreur", "ar": "خطأ"},
    "deg":           {"en": "DEG", "fr": "DEG", "ar": "درجة"},
    "rad":           {"en": "RAD", "fr": "RAD", "ar": "راديان"},

    # ── Converter ─────────────────────────────────────────────────
    "from":     {"en": "From", "fr": "De", "ar": "من"},
    "to":       {"en": "To", "fr": "À", "ar": "إلى"},
    "swap":     {"en": "Swap", "fr": "Inverser", "ar": "تبديل"},
    "weight":   {"en": "Weight", "fr": "Poids", "ar": "الوزن"},
    "currency": {"en": "Currency", "fr": "Devise", "ar": "العملة"},
    "volume":   {"en": "Volume", "fr": "Volume", "ar": "الحجم"},
    "area":     {"en": "Area", "fr": "Surface", "ar": "المساحة"},
    "distance": {"en": "Distance", "fr": "Distance", "ar": "المسافة"},

    # ── Equations ─────────────────────────────────────────────────
    "eq_title":  {"en": "Equations", "fr": "Équations", "ar": "المعادلات"},
    "eq1_tab":   {"en": "1st degree  ax + b = 0", "fr": "1er degré  ax + b = 0",
                  "ar": "الدرجة الأولى  ax + b = 0"},
    "eq2_tab":   {"en": "2nd degree  ax² + bx + c = 0",
                  "fr": "2ème degré  ax² + bx + c = 0",
                  "ar": "الدرجة الثانية  ax² + bx + c = 0"},
    "eq_expr_tab": {"en": "Expression", "fr": "Expression", "ar": "تعبير"},
    "eq_system_tab": {"en": "System", "fr": "Système", "ar": "نظام"},
    "coeff_a":  {"en": "Coefficient a", "fr": "Coefficient a", "ar": "المعامل أ"},
    "coeff_b":  {"en": "Coefficient b", "fr": "Coefficient b", "ar": "المعامل ب"},
    "coeff_c":  {"en": "Coefficient c", "fr": "Coefficient c", "ar": "المعامل ج"},
    "solve":    {"en": "Solve", "fr": "Résoudre", "ar": "حل"},
    "inf_solutions": {"en": "Infinite solutions", "fr": "∞ solutions",
                      "ar": "حلول غير محدودة"},
    "no_solution":   {"en": "No solution", "fr": "Pas de solution",
                      "ar": "لا يوجد حل"},
    "invalid_input": {"en": "Invalid input", "fr": "Entrée invalide",
                      "ar": "إدخال غير صحيح"},
    "expression":    {"en": "Expression (use x as variable)",
                      "fr": "Expression (utilisez x comme variable)",
                      "ar": "التعبير (استخدم x كمتغير)"},
    "value_of_x":    {"en": "Value of x", "fr": "Valeur de x", "ar": "قيمة x"},
    "result":        {"en": "Result", "fr": "Résultat", "ar": "النتيجة"},
    "calculate":     {"en": "Calculate", "fr": "Calculer", "ar": "احسب"},
    "find_roots":    {"en": "Find roots", "fr": "Trouver les racines",
                      "ar": "إيجاد الجذور"},
    "interval":      {"en": "Interval", "fr": "Intervalle", "ar": "الفترة"},
    "system_size":   {"en": "Number of equations", "fr": "Nombre d'équations",
                      "ar": "عدد المعادلات"},
    "equation_n":    {"en": "Equation", "fr": "Équation", "ar": "معادلة"},

    # ── Graphing ──────────────────────────────────────────────────
    "expressions":   {"en": "Expressions", "fr": "Expressions", "ar": "التعابير"},
    "add_expression":{"en": "+ Add expression", "fr": "+ Ajouter une expression",
                      "ar": "+ إضافة تعبير"},
    "sliders":       {"en": "Sliders", "fr": "Curseurs", "ar": "أشرطة التمرير"},
    "reset_view":    {"en": "Reset view", "fr": "Réinitialiser", "ar": "إعادة ضبط"},
    "clear_all":     {"en": "Clear all", "fr": "Tout effacer", "ar": "مسح الكل"},
    "zoom_in":       {"en": "Zoom +", "fr": "Zoom +", "ar": "تكبير +"},
    "zoom_out":      {"en": "Zoom −", "fr": "Zoom −", "ar": "تصغير −"},
    "graph_examples":{"en": "Examples: y = x^2  |  y = sin(x)  |  x^2 + y^2 = 25  |  a = 3",
                      "fr": "Exemples: y = x^2  |  y = sin(x)  |  x^2 + y^2 = 25  |  a = 3",
                      "ar": "أمثلة: y = x^2  |  y = sin(x)  |  x^2 + y^2 = 25  |  a = 3"},

    # ── Formulas ──────────────────────────────────────────────────
    "formula_title": {"en": "Scientific Formulas", "fr": "Formules Scientifiques",
                      "ar": "الصيغ العلمية"},
    "formula_quadratic": {"en": "Quadratic Formula", "fr": "Formule du second degré",
                          "ar": "صيغة المعادلة التربيعية"},
    "formula_area_circle": {"en": "Area of Circle", "fr": "Aire du cercle",
                            "ar": "مساحة الدائرة"},
    "formula_area_rect": {"en": "Area of Rectangle", "fr": "Aire du rectangle",
                          "ar": "مساحة المستطيل"},
    "formula_area_triangle": {"en": "Area of Triangle", "fr": "Aire du triangle",
                              "ar": "مساحة المثلث"},
    "formula_volume_sphere": {"en": "Volume of Sphere", "fr": "Volume de la sphère",
                              "ar": "حجم الكرة"},
    "formula_volume_cyl": {"en": "Volume of Cylinder", "fr": "Volume du cylindre",
                           "ar": "حجم الأسطوانة"},
    "formula_ohm": {"en": "Ohm's Law (V=IR)", "fr": "Loi d'Ohm (V=IR)",
                    "ar": "قانون أوم (V=IR)"},
    "formula_force": {"en": "Force (F=ma)", "fr": "Force (F=ma)", "ar": "القوة (F=ma)"},
    "formula_kinetic": {"en": "Kinetic Energy", "fr": "Énergie cinétique",
                        "ar": "طاقة الحركة"},

    # ── Matrices ──────────────────────────────────────────────────
    "matrix_size":   {"en": "Matrix size (2, 3 or 4)", "fr": "Taille de la matrice (2, 3 ou 4)",
                      "ar": "حجم المصفوفة (2، 3 أو 4)"},
    "matrix_det":    {"en": "Determinant", "fr": "Déterminant", "ar": "المحدد"},
    "matrix_inv":    {"en": "Inverse", "fr": "Inverse", "ar": "المصفوفة المعكوسة"},
    "matrix_trans":  {"en": "Transpose", "fr": "Transposée", "ar": "المنقول"},
    "matrix_mul":    {"en": "A × B", "fr": "A × B", "ar": "A × B"},
    "matrix_add":    {"en": "A + B", "fr": "A + B", "ar": "A + B"},
    "matrix_pow":    {"en": "A power n", "fr": "A puissance n", "ar": "A أُس n"},
    "matrix_trace":  {"en": "Trace", "fr": "Trace", "ar": "ال أثر"},
    "matrix_rank":   {"en": "Rank", "fr": "Rang", "ar": "الرتبة"},
    "matrix_result": {"en": "Result", "fr": "Résultat", "ar": "النتيجة"},

    # ── Calculus ──────────────────────────────────────────────────
    "derivative":    {"en": "Derivative", "fr": "Dérivée", "ar": "المشتقة"},
    "integral":      {"en": "Integral", "fr": "Intégrale", "ar": "التكامل"},
    "antiderivative":{"en": "Antiderivative", "fr": "Primitive", "ar": "النprimitive"},
    "point":         {"en": "Point", "fr": "Point", "ar": "نقطة"},
    "lower_bound":   {"en": "Lower bound", "fr": "Borne inférieure", "ar": "الحد الأدنى"},
    "upper_bound":   {"en": "Upper bound", "fr": "Borne supérieure", "ar": "الحد الأعلى"},

    # ── Statistics ────────────────────────────────────────────────
    "data_input":    {"en": "Data (space or comma separated)",
                      "fr": "Données (séparées par espace ou virgule)",
                      "ar": "البيانات (مفصولة بمسافة أو فاصلة)"},
    "stat_mean":     {"en": "Mean", "fr": "Moyenne", "ar": "المتوسط"},
    "stat_median":   {"en": "Median", "fr": "Médiane", "ar": "الوسيط"},
    "stat_mode":     {"en": "Mode", "fr": "Mode", "ar": "المنوال"},
    "stat_stdev":    {"en": "Standard deviation", "fr": "Écart-type", "ar": "الانحراف المعياري"},
    "stat_variance": {"en": "Variance", "fr": "Variance", "ar": "التباين"},
    "stat_min":      {"en": "Minimum", "fr": "Minimum", "ar": "أدنى قيمة"},
    "stat_max":      {"en": "Maximum", "fr": "Maximum", "ar": "أقصى قيمة"},
    "stat_sum":      {"en": "Sum", "fr": "Somme", "ar": "المجموع"},
    "stat_range":    {"en": "Range", "fr": "Étendue", "ar": "المدى"},
    "stat_count":    {"en": "Count", "fr": "Effectif", "ar": "العدد"},
    "stat_percentile":{"en": "Percentile p", "fr": "Percentile p", "ar": "المئين p"},
    "stat_regression":{"en": "Linear regression (x, y pairs)",
                       "fr": "Régression linéaire (paires x, y)",
                       "ar": "الانحدار الخطي (أزواج x، y)"},
    "stat_slope":    {"en": "Slope", "fr": "Pente", "ar": "الميل"},
    "stat_intercept":{"en": "Intercept", "fr": "Ordonnée à l'origine", "ar": "الجزء الثابت"},
    "stat_r2":       {"en": "R²", "fr": "R²", "ar": "R²"},
    "stat_corr":     {"en": "Correlation", "fr": "Corrélation", "ar": "الارتباط"},
    "stat_summary":  {"en": "Summary", "fr": "Résumé", "ar": "ملخص"},
}


def translate(key, lang="fr"):
    """Return the translation of *key* in *lang* (falls back to English)."""
    entry = STRINGS.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get("en", key))
