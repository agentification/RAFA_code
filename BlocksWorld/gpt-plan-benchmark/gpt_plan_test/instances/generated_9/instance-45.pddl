

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(ontable b)
(ontable c)
(on d b)
(on e d)
(ontable f)
(on g h)
(on h f)
(ontable i)
(clear a)
(clear c)
(clear g)
(clear i)
)
(:goal
(and
(on a c)
(on b g)
(on d b)
(on e d)
(on f h)
(on g f)
(on h i))
)
)


