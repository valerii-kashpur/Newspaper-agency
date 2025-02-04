class SearchMixin:
    search_form_class = None
    search_field = None

    def get_queryset(self):
        queryset = super().get_queryset()

        search_field = self.get_search_field() if hasattr(self,
                                                          "get_search_field") else self.search_field

        if self.search_form_class and search_field:
            form = self.search_form_class(self.request.GET)
            if form.is_valid():
                search_value = form.cleaned_data.get("search_value", "")
                if search_value:
                    return queryset.filter(
                        **{f"{search_field}__icontains": search_value})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_by = self.request.GET.get("search_by",
                                         "last_name")  # По умолчанию "last_name"
        search_value = self.request.GET.get("search_value", "")

        if self.search_form_class:
            context["search_form"] = self.search_form_class(
                initial={"search_by": search_by, "search_value": search_value}
            )

        return context


class SearchByMixin:
    allowed_search_fields = []

    def get_search_field(self):
        search_by = self.request.GET.get("search_by")
        if search_by in self.allowed_search_fields:
            return search_by
        return self.allowed_search_fields[
            0] if self.allowed_search_fields else None
