# VSCode uses this file to create a development container, for you to customize and test API Logic Projects.
#
# Per .devcontainer/devcontainer.json, VSCode will offer to open your API Logic Server Project in this docker container
#    Same as: View > Command > Remote-Containers: Open Folder in Container.
#
# https://apilogicserver.github.io/Docs/DevOps-Docker/
#
# image refresh nudge: release 17.04.07 (forces re-pull of apilogicserver/api_logic_server:latest)
FROM apilogicserver/api_logic_server
USER api_logic_server
CMD ["bash"]
