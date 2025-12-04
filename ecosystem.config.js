module.exports = {
  apps: [
    {
      name: "panel-subli",
      script: "/var/www/clients/client0/web17/private/venv/bin/gunicorn",
      args: "-w 2 -b 127.0.0.1:2000 app:app",
      cwd: "/var/www/clients/client0/web17/web/pagina-subli_hp",
      interpreter: "none",   // importante: usa gunicorn directo, no node
      env: {
        FLASK_ENV: "production",
        PYTHONUNBUFFERED: "1"
      }
    }
  ]
}
