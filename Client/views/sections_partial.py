from django.shortcuts import render
from Admin_panel.helpers.client.Section import GetSecPosts, GetMostVisitedSection


def blogs(request):
    return render(request, "component/index/blogs.html", GetSecPosts("blogs"))


def mostVisited(request):
    return render(request, "component/index/most_visited.html", GetMostVisitedSection("most_visited"))
