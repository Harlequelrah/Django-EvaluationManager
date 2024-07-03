import './styles/main.scss';

// Exemple d'utilisation de Stimulus (à adapter selon votre besoin)
import { Application } from 'stimulus';
import { definitionsFromContext } from 'stimulus/webpack-helpers';

const application = Application.start();
const context = require.context('./controllers', true, /\.js$/);
application.load(definitionsFromContext(context));
