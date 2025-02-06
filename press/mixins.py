class SearchMixin:
    search_form_class = None
    search_field = None
    allowed_search_fields = None

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_form_class:
            form = self.search_form_class(self.request.GET)
            if form.is_valid():
                if self.allowed_search_fields:
                    search_by = form.cleaned_data.get("search_by", "")
                    search_value = form.cleaned_data.get("search_value", "")

                    if search_by in self.allowed_search_fields and search_value:
                        return queryset.filter(
                            **{f"{search_by}__icontains": search_value})

                elif self.search_field:
                    search_value = form.cleaned_data.get(self.search_field, "")
                    if search_value:
                        return queryset.filter(**{
                            f"{self.search_field}__icontains": search_value})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.allowed_search_fields:
            search_by = self.request.GET.get("search_by",
                                             self.allowed_search_fields[0])
            search_value = self.request.GET.get("search_value", "")

            if self.search_form_class:
                context["search_form"] = self.search_form_class(
                    initial={"search_by": search_by,
                             "search_value": search_value}
                )

        elif self.search_field:
            search_value = self.request.GET.get(self.search_field, "")

            if self.search_form_class:
                context["search_form"] = self.search_form_class(
                    initial={self.search_field: search_value}
                )

        return context
